import { Mail, Github, Twitter } from "lucide-react";

const Footer = () => {
  return (
    <footer className="border-t border-border bg-card">
      <div className="container px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">HomeAnalyzer</h3>
            <p className="text-sm text-muted-foreground">
              AI-powered real estate analysis helping you find underpriced properties and make informed investment decisions.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="/analyze" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Analyze Property
                </a>
              </li>
              <li>
                <a href="/trends" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Market Trends
                </a>
              </li>
              <li>
                <a href="/about" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  About Us
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4 text-foreground">Connect</h3>
            <div className="flex space-x-4">
              <a
                href="mailto:contact@homeanalyzer.com"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                <Twitter className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
          © 2024 HomeAnalyzer. All rights reserved. | Powered by AI
        </div>
      </div>
    </footer>
  );
};

export default Footer;
