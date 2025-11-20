import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { Brain, Database, TrendingUp, Shield, ArrowRight } from "lucide-react";

const About = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "Custom AI Model",
      description: "Our proprietary machine learning model is trained on millions of real estate transactions, continuously learning and improving its predictions.",
    },
    {
      icon: Database,
      title: "Comprehensive Data",
      description: "We aggregate data from MLS listings, public records, market trends, and neighborhood analytics to provide the most accurate valuations.",
    },
    {
      icon: TrendingUp,
      title: "95% Accuracy Rate",
      description: "Through rigorous testing and validation, our model achieves 95% accuracy in predicting property values across diverse markets.",
    },
    {
      icon: Shield,
      title: "Trusted by Investors",
      description: "Used by professional real estate investors and agents to identify opportunities and make data-driven investment decisions.",
    },
  ];

  return (
    <div className="py-12">
      <div className="container px-4 max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 text-foreground">
            AI-Powered Real Estate Intelligence
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            HomeAnalyzer uses advanced machine learning to help investors and homebuyers identify underpriced properties and make smarter real estate decisions.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="p-8 hover:shadow-lg transition-shadow">
                <div className="flex items-start space-x-4">
                  <div className="rounded-lg bg-primary/10 p-4">
                    <Icon className="h-8 w-8 text-primary" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold mb-2 text-foreground">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* How It Works */}
        <Card className="p-8 mb-16">
          <h2 className="text-3xl font-bold mb-8 text-center text-foreground">How It Works</h2>
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-foreground">Data Collection</h3>
                <p className="text-muted-foreground">
                  Our system continuously collects and processes data from multiple sources including MLS listings, county records, and market analytics.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-foreground">AI Analysis</h3>
                <p className="text-muted-foreground">
                  When you input a property, our AI model analyzes hundreds of factors including location, size, condition, comparable sales, and market trends.
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-foreground">Deal Score & Insights</h3>
                <p className="text-muted-foreground">
                  Receive a comprehensive analysis including our proprietary deal score, predicted value, key value drivers, and actionable insights.
                </p>
              </div>
            </div>
          </div>
        </Card>

        {/* Stats */}
        <Card className="p-8 mb-16 bg-gradient-to-br from-primary/5 to-secondary/5">
          <h2 className="text-3xl font-bold mb-8 text-center text-foreground">Our Impact</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary mb-2">10,000+</div>
              <div className="text-muted-foreground">Properties Analyzed</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-secondary mb-2">95%</div>
              <div className="text-muted-foreground">Accuracy Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-info mb-2">$2B+</div>
              <div className="text-muted-foreground">Property Value Analyzed</div>
            </div>
          </div>
        </Card>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4 text-foreground">Ready to Find Your Next Deal?</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Start analyzing properties now and discover underpriced opportunities
          </p>
          <Button size="lg" onClick={() => navigate("/analyze")} className="font-semibold text-lg px-8">
            Analyze a Property
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default About;
