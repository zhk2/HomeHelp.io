import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AnalysisResponse, formatCurrency, formatNumber } from "@/lib/api";
import DealScoreGauge from "./DealScoreGauge";
import ValueDriversChart from "./ValueDriversChart";
import { ArrowDown, ArrowUp, RefreshCw } from "lucide-react";

interface AnalysisResultsProps {
  data: AnalysisResponse;
  onReset: () => void;
}

const AnalysisResults = ({ data, onReset }: AnalysisResultsProps) => {
  const { analysis, property, comparables } = data;
  const priceDiff = property.price - analysis.predicted_value;
  const priceDiffPercent = (priceDiff / property.price) * 100;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Property Summary */}
      <Card className="p-6">
        <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-2">{property.address}</h2>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">{property.property_type || "House"}</Badge>
              <Badge variant="outline">{property.bedrooms} bed</Badge>
              <Badge variant="outline">{property.bathrooms} bath</Badge>
              <Badge variant="outline">{formatNumber(property.sqft)} sqft</Badge>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-primary">{formatCurrency(property.price)}</div>
            <div className="text-sm text-muted-foreground">Listed Price</div>
          </div>
        </div>
      </Card>

      {/* Deal Score and Price Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DealScoreGauge score={analysis.deal_score} />
        
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-6 text-foreground">Price Comparison</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center pb-4 border-b border-border">
              <span className="text-muted-foreground">Listed Price</span>
              <span className="text-xl font-semibold">{formatCurrency(property.price)}</span>
            </div>
            <div className="flex justify-between items-center pb-4 border-b border-border">
              <span className="text-muted-foreground">AI Predicted Value</span>
              <span className="text-xl font-semibold text-primary">{formatCurrency(analysis.predicted_value)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="font-medium">Difference</span>
              <div className="text-right">
                <div className={`text-xl font-bold flex items-center gap-2 ${priceDiff > 0 ? 'text-destructive' : 'text-success'}`}>
                  {priceDiff > 0 ? <ArrowUp className="h-5 w-5" /> : <ArrowDown className="h-5 w-5" />}
                  {formatCurrency(Math.abs(priceDiff))}
                </div>
                <div className={`text-sm ${priceDiff > 0 ? 'text-destructive' : 'text-success'}`}>
                  {Math.abs(priceDiffPercent).toFixed(1)}% {priceDiff > 0 ? 'overpriced' : 'underpriced'}
                </div>
              </div>
            </div>
            <div className="pt-4 border-t border-border grid grid-cols-2 gap-4 text-sm">
              <div>
                <div className="text-muted-foreground">Price/sqft</div>
                <div className="font-semibold">${analysis.price_per_sqft}/sqft</div>
              </div>
              <div>
                <div className="text-muted-foreground">Predicted Price/sqft</div>
                <div className="font-semibold text-primary">${analysis.predicted_price_per_sqft}/sqft</div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Value Drivers and AI Explanation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ValueDriversChart drivers={analysis.value_drivers} />
        
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4 text-foreground">AI Analysis</h3>
          <p className="text-muted-foreground mb-4 leading-relaxed">{analysis.explanation}</p>
          <div className="space-y-2">
            <h4 className="font-semibold text-sm text-foreground">Key Factors:</h4>
            <div className="flex flex-wrap gap-2">
              {analysis.key_factors.map((factor, index) => (
                <Badge key={index} variant="secondary">
                  {factor}
                </Badge>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* Comparable Sales */}
      {comparables && comparables.length > 0 && (
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4 text-foreground">Comparable Sales</h3>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Address</TableHead>
                  <TableHead>Sale Price</TableHead>
                  <TableHead>Sale Date</TableHead>
                  <TableHead>Sqft</TableHead>
                  <TableHead>Bed/Bath</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {comparables.map((comp, index) => (
                  <TableRow key={index}>
                    <TableCell className="font-medium">{comp.address}</TableCell>
                    <TableCell>{formatCurrency(comp.sale_price)}</TableCell>
                    <TableCell>{new Date(comp.sale_date).toLocaleDateString()}</TableCell>
                    <TableCell>{formatNumber(comp.sqft)}</TableCell>
                    <TableCell>{comp.bedrooms} / {comp.bathrooms}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 justify-center">
        <Button onClick={onReset} size="lg" className="font-semibold">
          <RefreshCw className="mr-2 h-5 w-5" />
          Analyze Another Property
        </Button>
      </div>
    </div>
  );
};

export default AnalysisResults;
