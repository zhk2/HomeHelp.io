import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { Brain, TrendingDown, MapPin, LineChart, ArrowRight, CheckCircle2 } from "lucide-react";

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI Price Prediction",
      description: "Get accurate value estimates using machine learning trained on thousands of properties",
      color: "text-primary",
    },
    {
      icon: TrendingDown,
      title: "Deal Detection",
      description: "Find underpriced properties before others do with our proprietary scoring system",
      color: "text-secondary",
    },
    {
      icon: MapPin,
      title: "Neighborhood Analysis",
      description: "Understand market trends and value drivers in any location",
      color: "text-info",
    },
    {
      icon: LineChart,
      title: "Investment Insights",
      description: "Make informed real estate decisions backed by data and AI analysis",
      color: "text-warning",
    },
  ];

  const stats = [
    { value: "10,000+", label: "Properties Analyzed" },
    { value: "95%", label: "Accuracy Rate" },
    { value: "$2B+", label: "Property Value Analyzed" },
  ];

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/5 via-background to-secondary/5 py-20 md:py-32">
        <div className="container px-4">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-6 inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
              <CheckCircle2 className="mr-2 h-4 w-4" />
              AI-Powered Real Estate Analysis
            </div>
            <h1 className="mb-6 text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl md:text-6xl lg:text-7xl">
              Find Underpriced Homes with{" "}
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                AI-Powered Analysis
              </span>
            </h1>
            <p className="mb-8 text-lg text-muted-foreground md:text-xl">
              Our custom AI model analyzes property values, detects deals, and provides neighborhood insights to help you make smarter investment decisions
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                onClick={() => navigate("/analyze")}
                className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-lg px-8 py-6"
              >
                Analyze Property
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => navigate("/about")}
                className="font-semibold text-lg px-8 py-6"
              >
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y border-border bg-card py-12">
        <div className="container px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            {stats.map((stat, index) => (
              <div key={index} className="space-y-2">
                <div className="text-4xl font-bold text-primary">{stat.value}</div>
                <div className="text-sm text-muted-foreground uppercase tracking-wide">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4 md:text-4xl">
              Powerful Features for Smart Investors
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Everything you need to analyze properties and find the best deals in the market
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="p-6 hover:shadow-lg transition-shadow duration-300 border-border">
                  <div className="flex items-start space-x-4">
                    <div className={`rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 p-3 ${feature.color}`}>
                      <Icon className="h-6 w-6" />
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
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-br from-primary to-secondary py-20">
        <div className="container px-4 text-center">
          <h2 className="text-3xl font-bold text-primary-foreground mb-4 md:text-4xl">
            Ready to Find Your Next Investment?
          </h2>
          <p className="text-lg text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
            Start analyzing properties now and discover underpriced opportunities before anyone else
          </p>
          <Button
            size="lg"
            variant="secondary"
            onClick={() => navigate("/analyze")}
            className="font-semibold text-lg px-8 py-6"
          >
            Start Analyzing
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
