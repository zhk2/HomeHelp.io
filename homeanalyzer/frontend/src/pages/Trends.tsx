import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { getNeighborhoodTrends, TrendsResponse, formatCurrency } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Search, TrendingUp, Clock, DollarSign, Activity } from "lucide-react";

const Trends = () => {
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [trendsData, setTrendsData] = useState<TrendsResponse | null>(null);
  const { toast } = useToast();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!address.trim()) {
      toast({
        title: "Address Required",
        description: "Please enter a city or zip code",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const result = await getNeighborhoodTrends(address);
      setTrendsData(result);
      toast({
        title: "Trends Loaded",
        description: `Market data for ${result.location} retrieved successfully.`,
      });
    } catch (err) {
      toast({
        title: "Failed to Load Trends",
        description: err instanceof Error ? err.message : "Network error",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-12">
      <div className="container px-4 max-w-6xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Neighborhood Trends</h1>
          <p className="text-lg text-muted-foreground">
            Explore real estate market trends and statistics for any location
          </p>
        </div>

        <Card className="p-6 mb-8">
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="search" className="text-base font-semibold">
                Enter City or ZIP Code
              </Label>
              <div className="flex gap-4">
                <Input
                  id="search"
                  placeholder="San Francisco, CA or 94102"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="flex-1"
                  disabled={loading}
                />
                <Button type="submit" disabled={loading} size="lg">
                  <Search className="mr-2 h-5 w-5" />
                  Search
                </Button>
              </div>
            </div>
          </form>
        </Card>

        {trendsData && (
          <div className="space-y-6 animate-in fade-in duration-500">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <DollarSign className="h-8 w-8 text-primary" />
                </div>
                <div className="text-2xl font-bold text-foreground">{formatCurrency(trendsData.average_price)}</div>
                <div className="text-sm text-muted-foreground">Average Home Price</div>
              </Card>

              <Card className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <Clock className="h-8 w-8 text-secondary" />
                </div>
                <div className="text-2xl font-bold text-foreground">{trendsData.days_on_market} days</div>
                <div className="text-sm text-muted-foreground">Avg Days on Market</div>
              </Card>

              <Card className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <TrendingUp className="h-8 w-8 text-info" />
                </div>
                <div className="text-2xl font-bold text-foreground">${trendsData.price_per_sqft}/sqft</div>
                <div className="text-sm text-muted-foreground">Price per Square Foot</div>
              </Card>

              <Card className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <Activity className="h-8 w-8 text-warning" />
                </div>
                <div className="text-2xl font-bold text-foreground capitalize">{trendsData.market_status}</div>
                <div className="text-sm text-muted-foreground">Market Status</div>
              </Card>
            </div>

            <Card className="p-6">
              <h3 className="text-xl font-semibold mb-6 text-foreground">Price Trends (6 Months)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trendsData.price_trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" />
                  <YAxis stroke="hsl(var(--muted-foreground))" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "0.5rem",
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="hsl(var(--primary))"
                    strokeWidth={3}
                    dot={{ fill: "hsl(var(--primary))", r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Card>

            <Card className="p-6 bg-gradient-to-br from-primary/5 to-secondary/5">
              <h3 className="text-xl font-semibold mb-4 text-foreground">Market Insights</h3>
              <div className="space-y-2 text-muted-foreground">
                <p>• Total sales volume in the past 6 months: {trendsData.total_sales} properties</p>
                <p>• Current market conditions favor: {trendsData.market_status === "buyer" ? "Buyers" : "Sellers"}</p>
                <p>• Average time to sell has been {trendsData.days_on_market} days</p>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default Trends;
