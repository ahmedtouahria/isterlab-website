import json
from django.shortcuts import render
from .models import Category
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def chatbot_view(request):
    def build_conversation_flow(category, parent_id=None):
        flow = {
            "message": category.message or f"Here are options for {category.name}:",
            "options": {}
        }
        
        # Add subcategories as options
        for subcategory in category.subcategories.all():
            flow["options"][f"category_{subcategory.id}"] = {
                "text": subcategory.name,
                "type": "category",
                "id": subcategory.id
            }
        
        # Add responses as options
        for response in category.responses.all():
            flow["options"][f"response_{response.id}"] = {
                "text": response.response,
                "type": "response",
                "id": response.id
            }
            
            # Add linked blogs if they exist
            if response.blogs.exists():
                flow["options"][f"response_{response.id}"]["blogs"] = [
                    {
                        "id": blog.id,
                        "title": blog.title,
                        "url": blog.get_absolute_url()  # Assuming your Blog model has this
                    } for blog in response.blogs.all()
                ]
        
        # Add back button if not root
        if parent_id:
            flow["options"]["back"] = {
                "text": "← Back",
                "type": "back",
                "target": parent_id
            }
        else:
            flow["options"]["back"] = {
                "text": "← Main Menu",
                "type": "back",
                "target": None
            }
        
        return flow

    # Get root categories (where parent is None)
    root_categories = Category.objects.filter(parent__isnull=True)
    
    # Build complete conversation flow
    conversation_flow = {}
    
    # First build all categories recursively
    def process_category(category, parent_id=None):
        flow = build_conversation_flow(category, parent_id)
        conversation_flow[f"category_{category.id}"] = flow
        
        for subcategory in category.subcategories.all():
            process_category(subcategory, parent_id=category.id)
    
    for root_category in root_categories:
        process_category(root_category)
    
    # Add main menu
    conversation_flow["init"] = {
        "message": "How can I help you today?",
        "options": {
            f"category_{cat.id}": {
                "text": cat.name,
                "type": "category",
                "id": cat.id
            } for cat in root_categories
        }
    }
    
    # Add back handler
    conversation_flow["back"] = {
        "message": "What else can I help you with?",
        "options": {
            f"category_{cat.id}": {
                "text": cat.name,
                "type": "category",
                "id": cat.id
            } for cat in root_categories
        }
    }
    
    context = {
        'conversation_flow_json': json.dumps(conversation_flow, cls=DjangoJSONEncoder)
        }
    return render(request, 'chatbot/home.html',context)