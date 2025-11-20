import { useState } from "react";
import PropertyForm from "@/components/PropertyForm";
import AnalysisResults from "@/components/AnalysisResults";
import { analyzeProperty, AnalysisResponse, PropertyData } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

const Analysis = () => {
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (propertyData: PropertyData) => {
    setLoading(true);
    setError(null);

    try {
      const result = await analyzeProperty(propertyData);
      setAnalysisData(result);
      toast({
        title: "Analysis Complete",
        description: "Your property has been successfully analyzed.",
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to analyze property";
      setError(errorMessage);
      toast({
        title: "Analysis Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisData(null);
    setError(null);
  };

  return (
    <div className="py-12">
      <div className="container px-4 max-w-6xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Property Analysis</h1>
          <p className="text-lg text-muted-foreground">
            Enter property details below to get AI-powered valuation and deal score
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {!analysisData ? (
          <PropertyForm onSubmit={handleSubmit} loading={loading} />
        ) : (
          <AnalysisResults data={analysisData} onReset={handleReset} />
        )}
      </div>
    </div>
  );
};

export default Analysis;
