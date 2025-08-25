#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deployment Status Checker
Monitor the health and status of your deployed Hudhud KPI System
"""

import requests
import json
import time
import sys
from datetime import datetime

class DeploymentChecker:
    def __init__(self, base_url=None):
        """Initialize deployment checker with optional base URL"""
        self.base_url = base_url or "https://portall-nn5x.onrender.com"
        self.health_endpoints = ["/health", "/healthz"]
        
    def check_health(self, endpoint):
        """Check a specific health endpoint"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "data": data
                }
            else:
                return {
                    "status": "unhealthy",
                    "response_time": None,
                    "error": f"HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "response_time": None,
                "error": str(e)
            }
    
    def check_all_endpoints(self):
        """Check all health endpoints"""
        results = {}
        for endpoint in self.health_endpoints:
            results[endpoint] = self.check_health(endpoint)
        return results
    
    def display_status(self, results):
        """Display health check results in a nice format"""
        print(f"\n🏥 Health Check Results for {self.base_url}")
        print("=" * 60)
        print(f"⏰ Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        overall_healthy = True
        
        for endpoint, result in results.items():
            status = result["status"]
            if status == "healthy":
                print(f"✅ {endpoint:<10} - HEALTHY")
                print(f"   Response time: {result['response_time']:.3f}s")
                print(f"   Service: {result['data'].get('service', 'Unknown')}")
            elif status == "unhealthy":
                print(f"❌ {endpoint:<10} - UNHEALTHY")
                print(f"   Error: {result['error']}")
                overall_healthy = False
            else:
                print(f"🔌 {endpoint:<10} - CONNECTION ERROR")
                print(f"   Error: {result['error']}")
                overall_healthy = False
            print()
        
        if overall_healthy:
            print("🎉 All endpoints are healthy!")
        else:
            print("⚠️  Some endpoints have issues")
        
        return overall_healthy
    
    def monitor(self, interval=30, max_checks=None):
        """Continuously monitor the deployment"""
        print(f"🔄 Starting continuous monitoring (checking every {interval}s)")
        print("Press Ctrl+C to stop")
        
        check_count = 0
        try:
            while True:
                if max_checks and check_count >= max_checks:
                    break
                
                results = self.check_all_endpoints()
                self.display_status(results)
                
                check_count += 1
                if max_checks:
                    remaining = max_checks - check_count
                    print(f"Remaining checks: {remaining}")
                
                if check_count < (max_checks or float('inf')):
                    print(f"⏳ Waiting {interval}s for next check...")
                    time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check deployment health status")
    parser.add_argument("--url", 
                       default="https://portall-nn5x.onrender.com",
                       help="Base URL of your deployed application")
    parser.add_argument("--monitor", 
                       action="store_true",
                       help="Continuously monitor the deployment")
    parser.add_argument("--interval", 
                       type=int, 
                       default=30,
                       help="Check interval in seconds (default: 30)")
    parser.add_argument("--max-checks", 
                       type=int,
                       help="Maximum number of checks in monitor mode")
    parser.add_argument("--local", 
                       action="store_true",
                       help="Check local development server (localhost:8050)")
    
    args = parser.parse_args()
    
    # Determine URL
    if args.local:
        url = "http://localhost:8050"
    else:
        url = args.url
    
    # Create checker
    checker = DeploymentChecker(url)
    
    if args.monitor:
        checker.monitor(args.interval, args.max_checks)
    else:
        # Single check
        results = checker.check_all_endpoints()
        healthy = checker.display_status(results)
        
        if not healthy:
            print("\n💡 Troubleshooting tips:")
            print("   • Check if the deployment is still in progress")
            print("   • Verify the URL is correct")
            print("   • Check Render dashboard for deployment logs")
            print("   • Ensure health endpoints are properly configured")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)