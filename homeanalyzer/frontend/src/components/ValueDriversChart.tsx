import { Card } from "@/components/ui/card";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

interface ValueDriversChartProps {
  drivers: {
    location: number;
    size: number;
    condition: number;
    market_timing: number;
  };
}

const ValueDriversChart = ({ drivers }: ValueDriversChartProps) => {
  const data = [
    { name: "Location", value: drivers.location, color: "hsl(var(--primary))" },
    { name: "Size", value: drivers.size, color: "hsl(var(--secondary))" },
    { name: "Condition", value: drivers.condition, color: "hsl(var(--info))" },
    { name: "Market Timing", value: drivers.market_timing, color: "hsl(var(--warning))" },
  ];

  return (
    <Card className="p-6">
      <h3 className="text-xl font-semibold mb-6 text-foreground">Value Drivers</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `${value}%`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default ValueDriversChart;
