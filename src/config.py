"""
Configuration constants for the Geminicli2api proxy server.
Centralizes all configuration to avoid duplication across modules.
"""
import os

# API Endpoints
CODE_ASSIST_ENDPOINT = "https://cloudcode-pa.googleapis.com"

# Client Configuration
CLI_VERSION = "0.1.5"  # Match current gemini-cli version

# OAuth Configuration
CLIENT_ID = "681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# File Paths
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIAL_FILE = os.path.join(SCRIPT_DIR, os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "oauth_creds.json"))

# Authentication
GEMINI_AUTH_PASSWORD = os.getenv("GEMINI_AUTH_PASSWORD", "123456")

# Default Safety Settings for Google API
DEFAULT_SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_IMAGE_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_IMAGE_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_IMAGE_HATE", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_IMAGE_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_UNSPECIFIED", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_JAILBREAK", "threshold": "BLOCK_NONE"}
]

# Base Models (without search variants)
BASE_MODELS = [
    {
        "name": "models/gemini-2.5-pro",
        "version": "001",
        "displayName": "Gemini 2.5 Pro",
        "description": "Advanced multimodal model with enhanced capabilities",
        "inputTokenLimit": 1048576,
        "outputTokenLimit": 65535,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    },
    {
        "name": "models/gemini-2.5-flash",
        "version": "001",
        "displayName": "Gemini 2.5 Flash",
        "description": "Fast and efficient multimodal model with latest improvements",
        "inputTokenLimit": 1048576,
        "outputTokenLimit": 65535,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    },
    {
        "name": "models/gemini-2.5-flash-image-preview",
        "version": "001",
        "displayName": "Gemini 2.5 Flash Image Preview",
        "description": "Gemini 2.5 Flash Image Preview",
        "inputTokenLimit": 32768,
        "outputTokenLimit": 32768,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    },
    {
        "name": "models/gemini-3-pro-preview",
        "version": "001",
        "displayName": "Gemini 3.0 Pro Preview",
        "description": "Preview version of Gemini 3.0 Pro",
        "inputTokenLimit": 2097152,
        "outputTokenLimit": 65535,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    },
    {
        "name": "models/gemini-3.1-pro-preview",
        "version": "001",
        "displayName": "Gemini 3.1 Pro Preview",
        "description": "Preview version of Gemini 3.1 Pro",
        "inputTokenLimit": 2097152,
        "outputTokenLimit": 65535,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    },
    {
        "name": "models/gemini-3-flash-preview",
        "version": "001",
        "displayName": "Gemini 3.0 Flash Preview",
        "description": "Preview version of Gemini 3.0 Flash",
        "inputTokenLimit": 1048576,
        "outputTokenLimit": 65535,
        "supportedGenerationMethods": ["generateContent", "streamGenerateContent"],
        "temperature": 1.0,
        "maxTemperature": 2.0,
        "topP": 0.95,
        "topK": 64
    }
]

# Generate search variants for applicable models
def _generate_search_variants():
    """Generate search variants for models that support content generation."""
    search_models = []
    base_model_with_variance = [model for model in BASE_MODELS if "gemini-2.5-flash-image" not in model["name"]]
    for model in base_model_with_variance:
        if "generateContent" in model["supportedGenerationMethods"]:
            search_variant = model.copy()
            search_variant["name"] = model["name"] + "-search"
            search_variant["displayName"] = model["displayName"] + " with Google Search"
            search_variant["description"] = model["description"] + " (includes Google Search grounding)"
            search_models.append(search_variant)
    return search_models

# Generate thinking variants for applicable models
def _generate_thinking_variants():
    """Generate nothinking and maxthinking variants for models that support thinking."""
    thinking_models = []
    base_model_with_variance = [model for model in BASE_MODELS if "gemini-2.5-flash-image" not in model["name"]]
    for model in base_model_with_variance:
        # Check if the model is 2.5 or any 3.x model
        if ("generateContent" in model["supportedGenerationMethods"] and
            ("gemini-2.5-flash" in model["name"] or "gemini-2.5-pro" in model["name"] or "gemini-3" in model["name"])):
            
            # Add -nothinking variant
            nothinking_variant = model.copy()
            nothinking_variant["name"] = model["name"] + "-nothinking"
            nothinking_variant["displayName"] = model["displayName"] + " (No Thinking)"
            nothinking_variant["description"] = model["description"] + " (thinking disabled)"
            thinking_models.append(nothinking_variant)
            
            # Add -maxthinking variant
            maxthinking_variant = model.copy()
            maxthinking_variant["name"] = model["name"] + "-maxthinking"
            maxthinking_variant["displayName"] = model["displayName"] + " (Max Thinking)"
            maxthinking_variant["description"] = model["description"] + " (maximum thinking budget)"
            thinking_models.append(maxthinking_variant)
    return thinking_models

# Generate combined variants (search + thinking combinations)
def _generate_combined_variants():
    """Generate combined search and thinking variants."""
    combined_models = []
    for model in BASE_MODELS:
        if ("generateContent" in model["supportedGenerationMethods"] and
            ("gemini-2.5-flash" in model["name"] or "gemini-2.5-pro" in model["name"] or "gemini-3" in model["name"])):
            
            # search + nothinking
            search_nothinking = model.copy()
            search_nothinking["name"] = model["name"] + "-search-nothinking"
            search_nothinking["displayName"] = model["displayName"] + " with Google Search (No Thinking)"
            search_nothinking["description"] = model["description"] + " (includes Google Search grounding, thinking disabled)"
            combined_models.append(search_nothinking)
            
            # search + maxthinking
            search_maxthinking = model.copy()
            search_maxthinking["name"] = model["name"] + "-search-maxthinking"
            search_maxthinking["displayName"] = model["displayName"] + " with Google Search (Max Thinking)"
            search_maxthinking["description"] = model["description"] + " (includes Google Search grounding, maximum thinking budget)"
            combined_models.append(search_maxthinking)
    return combined_models

# Combine all models and then sort them by name to group variants together
all_models = BASE_MODELS + _generate_search_variants() + _generate_thinking_variants() + _generate_combined_variants()
SUPPORTED_MODELS = sorted(all_models, key=lambda x: x['name'])

# Helper function to get base model name from any variant
def get_base_model_name(model_name):
    """Convert variant model name to base model name."""
    suffixes = ["-search-maxthinking", "-search-nothinking", "-maxthinking", "-nothinking", "-search"]
    for suffix in suffixes:
        if model_name.endswith(suffix):
            return model_name[:-len(suffix)]
    return model_name

def is_search_model(model_name):
    return "-search" in model_name

def is_nothinking_model(model_name):
    return "-nothinking" in model_name

def is_maxthinking_model(model_name):
    return "-maxthinking" in model_name

def get_thinking_budget(model_name):
    """Get the appropriate thinking budget for a model based on its name and variant."""
    base_model = get_base_model_name(model_name)
    
    if is_nothinking_model(model_name):
        if "flash" in base_model:
            return 0  # No thinking for flash
        elif "pro" in base_model:
            return 128  # Limited thinking for pro
    elif is_maxthinking_model(model_name):
        if "flash" in base_model:
            return 24576
        elif "pro" in base_model:
            return 32768 # Works for 2.5, 3.0, and 3.1 pro
    return -1  # Default for all models

def should_include_thoughts(model_name):
    """Check if thoughts should be included in the response."""
    if is_nothinking_model(model_name):
        base_model = get_base_model_name(model_name)
        return "pro" in base_model # All pro models include thoughts
    return True
