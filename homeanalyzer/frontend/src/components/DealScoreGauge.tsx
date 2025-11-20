import { Card } from "@/components/ui/card";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";

interface DealScoreGaugeProps {
  score: number;
}

const DealScoreGauge = ({ score }: DealScoreGaugeProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 8) return "hsl(var(--success))";
    if (score >= 6) return "hsl(var(--primary))";
    if (score >= 4) return "hsl(var(--warning))";
    return "hsl(var(--destructive))";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 8) return "Excellent Deal";
    if (score >= 6) return "Fair Price";
    if (score >= 4) return "Overpriced";
    return "Avoid";
  };

  const percentage = (score / 10) * 100;
  const data = [
    { value: percentage, fill: getScoreColor(score) },
    { value: 100 - percentage, fill: "hsl(var(--muted))" },
  ];

  return (
    <Card className="p-6">
      <h3 className="text-xl font-semibold mb-6 text-center text-foreground">Deal Score</h3>
      <div className="relative">
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              startAngle={180}
              endAngle={0}
              innerRadius={60}
              outerRadius={80}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center mt-8">
          <div className="text-5xl font-bold" style={{ color: getScoreColor(score) }}>
            {score.toFixed(1)}
          </div>
          <div className="text-sm text-muted-foreground font-medium">/10</div>
        </div>
      </div>
      <div className="mt-6 text-center">
        <div className="inline-flex items-center justify-center px-4 py-2 rounded-full font-semibold text-sm"
             style={{ 
               backgroundColor: `${getScoreColor(score)}15`,
               color: getScoreColor(score)
             }}>
          {getScoreLabel(score)}
        </div>
      </div>
    </Card>
  );
};

export default DealScoreGauge;
