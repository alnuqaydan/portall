#!/bin/bash
# Quick Deploy Script for Hudhud KPI System on Render
# This script automates the deployment process

set -e

echo "🚀 Hudhud KPI System - Quick Deploy Script"
echo "==========================================="

# Function to check if we're in the right directory
check_directory() {
    if [[ ! -f "app.py" ]] || [[ ! -f "render.yaml" ]]; then
        echo "❌ Error: Please run this script from the project root directory"
        echo "   (Directory should contain app.py and render.yaml)"
        exit 1
    fi
}

# Function to validate deployment readiness
validate_deployment() {
    echo "🔍 Validating deployment readiness..."
    
    if command -v python3 &> /dev/null; then
        python3 deploy_render.py --skip-deps
    elif command -v python &> /dev/null; then
        python deploy_render.py --skip-deps
    else
        echo "❌ Python not found. Please install Python 3.8+"
        exit 1
    fi
    
    validation_result=$?
    if [ $validation_result -ne 0 ]; then
        echo "⚠️  Validation warnings detected, but continuing with deployment..."
    fi
}

# Function to commit and push changes
deploy_to_git() {
    echo "📤 Preparing Git deployment..."
    
    # Check if git repo is initialized
    if [[ ! -d ".git" ]]; then
        echo "❌ Error: Not a Git repository. Please initialize Git first:"
        echo "   git init"
        echo "   git remote add origin <your-repo-url>"
        exit 1
    fi
    
    # Check for uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        echo "📝 Found uncommitted changes. Committing..."
        git add .
        
        # Get commit message from user or use default
        if [[ -n "$1" ]]; then
            commit_message="$1"
        else
            commit_message="Deploy: Optimized for Render deployment $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        
        git commit -m "$commit_message"
        echo "✅ Changes committed: $commit_message"
    else
        echo "ℹ️  No uncommitted changes found"
    fi
    
    # Push to remote
    current_branch=$(git branch --show-current)
    echo "🚀 Pushing to origin/$current_branch..."
    
    if git push origin "$current_branch"; then
        echo "✅ Successfully pushed to Git repository"
    else
        echo "⚠️  Push failed. This might be due to:"
        echo "   - Network issues"
        echo "   - Authentication problems"
        echo "   - Remote repository not configured"
        echo "   Please check your Git configuration and try again"
        exit 1
    fi
}

# Function to display deployment instructions
show_render_instructions() {
    echo ""
    echo "🎯 Next Steps for Render Deployment:"
    echo "===================================="
    echo "1. 🌐 Go to https://dashboard.render.com"
    echo "2. 📊 Click 'New +' → 'Web Service'"
    echo "3. 🔗 Connect your Git repository"
    echo "4. ⚙️  Render should auto-detect render.yaml configuration"
    echo "5. 🚀 Click 'Create Web Service' to deploy"
    echo ""
    echo "📋 Your deployment configuration:"
    echo "   • Build Command: pip install -r requirements.txt"
    echo "   • Start Command: gunicorn app:app.server --config gunicorn.conf.py"
    echo "   • Health Check: /health"
    echo "   • Auto-Deploy: Enabled"
    echo ""
    echo "🔗 After deployment, your app will be available at:"
    echo "   https://your-service-name.onrender.com"
    echo ""
    echo "📈 Monitor deployment:"
    echo "   • Check build logs in Render dashboard"
    echo "   • Verify health endpoint: /health"
    echo "   • Monitor application logs for errors"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [options] [commit-message]"
    echo ""
    echo "Options:"
    echo "  --validate-only    Only run validation, don't deploy"
    echo "  --no-git          Skip Git operations"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Quick deploy with auto-generated commit message"
    echo "  $0 \"Add new KPI dashboard feature\"    # Deploy with custom commit message"
    echo "  $0 --validate-only                   # Only validate, don't push to Git"
    echo "  $0 --no-git                          # Skip Git push (for testing)"
}

# Main script execution
main() {
    # Parse command line arguments
    validate_only=false
    no_git=false
    commit_message=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --validate-only)
                validate_only=true
                shift
                ;;
            --no-git)
                no_git=true
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                if [[ -z "$commit_message" ]]; then
                    commit_message="$1"
                fi
                shift
                ;;
        esac
    done
    
    # Check directory
    check_directory
    
    # Always validate
    validate_deployment
    
    if [[ "$validate_only" == true ]]; then
        echo "✅ Validation complete. Use without --validate-only to deploy."
        exit 0
    fi
    
    # Deploy to Git unless disabled
    if [[ "$no_git" != true ]]; then
        deploy_to_git "$commit_message"
    else
        echo "⏭️  Skipping Git operations (--no-git flag)"
    fi
    
    # Show next steps
    show_render_instructions
    
    echo ""
    echo "🎉 Quick deploy script completed successfully!"
    echo "💡 Monitor the Render dashboard for deployment progress"
}

# Run main function with all arguments
main "$@"