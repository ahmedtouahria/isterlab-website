import json
from django.shortcuts import render
from django.urls import reverse
from landing.models import *
from django.core.cache import cache
# Create your views here.
def build_conversation_flow():
    
    def get_absolute_url_for_model(model, obj):
        """Helper to generate URLs for different models"""
        if model == 'service':
            return reverse('service_details', kwargs={'name': obj.name})
        elif model == 'solution':
            return reverse('solution_details', kwargs={'name': obj.name})
        elif model == 'blog':
            return reverse('blog_details', kwargs={'slug': obj.slug})
        return '#'
    
    # Initialize the conversation flow
    flow = {
        "init": {
            "message": "Welcome to our IT Solutions Chatbot. How can I help you today?",
            "options": {}
        }
    }
    
    # 1. Add Services
    services = Service.objects.all().prefetch_related('faqs')
    if services.exists():
        flow["services"] = {
            "message": "Our professional services include:",
            "options": {}
        }
        
        for service in services:
            key = f"service_{service.id}"
            flow[key] = {
                "message": f"{service.name}\n\n{service.short_description}",
                "options": {
                    "details": {
                        "text": "View Full Details",
                        "type": "url",
                        "url": get_absolute_url_for_model('service', service)
                    },
                    "back": {
                        "text": "← Back to Services",
                        "type": "back",
                        "target": "services"
                    }
                }
            }
            
            # Add FAQs if they exist
            if service.faqs.exists():
                flow[key]["options"]["faqs"] = {
                    "text": "FAQs",
                    "type": "category",
                    "target": f"service_faqs_{service.id}"
                }
                
                flow[f"service_faqs_{service.id}"] = {
                    "message": f"Frequently asked questions about {service.name}:",
                    "options": {}
                }
                
                for faq in service.faqs.all():
                    flow[f"service_faqs_{service.id}"]["options"][f"faq_{faq.id}"] = {
                        "text": faq.question,
                        "type": "response",
                        "response": faq.response
                    }
                
                flow[f"service_faqs_{service.id}"]["options"]["back"] = {
                    "text": "← Back to Service",
                    "type": "back",
                    "target": key
                }
            
            # Add to main services menu
            flow["services"]["options"][key] = {
                "text": service.name,
                "type": "category",
                "target": key
            }
        
        flow["init"]["options"]["services"] = {
            "text": "Our Services",
            "type": "category",
            "target": "services"
        }
    
    # 2. Add Solutions
    solutions = Solution.objects.all().prefetch_related('faqs')
    if solutions.exists():
        flow["solutions"] = {
            "message": "Our technical solutions include:",
            "options": {}
        }
        
        for solution in solutions:
            key = f"solution_{solution.id}"
            flow[key] = {
                "message": f"{solution.name}\n\n{solution.short_description}",
                "options": {
                    "details": {
                        "text": "View Full Details",
                        "type": "url",
                        "url": get_absolute_url_for_model('solution', solution)
                    },
                    "back": {
                        "text": "← Back to Solutions",
                        "type": "back",
                        "target": "solutions"
                    }
                }
            }
            
            # Add FAQs if they exist
            if solution.faqs.exists():
                flow[key]["options"]["faqs"] = {
                    "text": "FAQs",
                    "type": "category",
                    "target": f"solution_faqs_{solution.id}"
                }
                
                flow[f"solution_faqs_{solution.id}"] = {
                    "message": f"Frequently asked questions about {solution.name}:",
                    "options": {}
                }
                
                for faq in solution.faqs.all():
                    flow[f"solution_faqs_{solution.id}"]["options"][f"faq_{faq.id}"] = {
                        "text": faq.question,
                        "type": "response",
                        "response": faq.response
                    }
                
                flow[f"solution_faqs_{solution.id}"]["options"]["back"] = {
                    "text": "← Back to Solution",
                    "type": "back",
                    "target": key
                }
            
            # Add to main solutions menu
            flow["solutions"]["options"][key] = {
                "text": solution.name,
                "type": "category",
                "target": key
            }
        
        flow["init"]["options"]["solutions"] = {
            "text": "Our Solutions",
            "type": "category",
            "target": "solutions"
        }
    
    # 3. Add General FAQs
    general_faqs = FAQ.objects.all()
    if general_faqs.exists():
        flow["faqs"] = {
            "message": "Frequently asked questions:",
            "options": {}
        }
        
        for faq in general_faqs:
            flow["faqs"]["options"][f"faq_{faq.id}"] = {
                "text": faq.question,
                "type": "response",
                "response": faq.response
            }
        
        flow["faqs"]["options"]["back"] = {
            "text": "← Main Menu",
            "type": "back",
            "target": "init"
        }
        
        flow["init"]["options"]["faqs"] = {
            "text": "FAQs",
            "type": "category",
            "target": "faqs"
        }
    
    # 4. Add Brands
    brands = Brand.objects.all()
    if brands.exists():
        flow["brands"] = {
            "message": "We work with these trusted brands:",
            "options": {}
        }
        
        for brand in brands:
            flow["brands"]["options"][f"brand_{brand.id}"] = {
                "text": brand.name,
                "type": "response",
                "response": f"We provide solutions and support for {brand.name} products and systems."
            }
        
        flow["brands"]["options"]["back"] = {
            "text": "← Main Menu",
            "type": "back",
            "target": "init"
        }
        
        flow["init"]["options"]["brands"] = {
            "text": "Supported Brands",
            "type": "category",
            "target": "brands"
        }
    
    # 5. Add Contact Options
    flow["contact"] = {
        "message": "How would you like to contact us?",
        "options": {
            "email": {
                "text": "Email Us",
                "type": "url",
                "url": reverse('contact')
            },
            "partner": {
                "text": "Become a Partner",
                "type": "url",
                "url": reverse('become_a_partner')
            },
            "back": {
                "text": "← Main Menu",
                "type": "back",
                "target": "init"
            }
        }
    }
    
    flow["init"]["options"]["contact"] = {
        "text": "Contact Us",
        "type": "category",
        "target": "contact"
    }
    
    # 6. Add Back Handler
    flow["back"] = {
        "message": "What else can I help you with?",
        "options": flow["init"]["options"].copy()
    }
    
    return flow


def chatbot_view(request):

    conversationflow = cache.get("conversation_flow_v2")
    if not conversationflow :
        conversationflow =build_conversation_flow()
        cache.set("conversation_flow_v2",conversationflow)

    context = { 
        'conversation_flow_json':  conversationflow
        }
    return render(request, 'chatbot/home.html',context)