from django import forms


def validate_social_link(link, platform_name, data):
    if not f"{data}.com" in link:
        raise forms.ValidationError(f"Please enter a valid {platform_name} URL.")
    return link