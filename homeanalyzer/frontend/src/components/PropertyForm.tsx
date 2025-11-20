import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { PropertyData } from "@/lib/api";

interface PropertyFormProps {
  onSubmit: (data: PropertyData) => void;
  loading: boolean;
}

const PropertyForm = ({ onSubmit, loading }: PropertyFormProps) => {
  const [formData, setFormData] = useState<PropertyData>({
    address: "",
    price: 0,
    sqft: 0,
    bedrooms: 3,
    bathrooms: 2,
    year_built: new Date().getFullYear(),
    property_type: "House",
  });

  const [errors, setErrors] = useState<Partial<Record<keyof PropertyData, string>>>({});

  const validate = (): boolean => {
    const newErrors: Partial<Record<keyof PropertyData, string>> = {};

    if (!formData.address.trim()) {
      newErrors.address = "Address is required";
    }

    if (formData.price < 1000 || formData.price > 50000000) {
      newErrors.price = "Price must be between $1,000 and $50,000,000";
    }

    if (formData.sqft < 100 || formData.sqft > 50000) {
      newErrors.sqft = "Square feet must be between 100 and 50,000";
    }

    if (formData.year_built < 1800 || formData.year_built > new Date().getFullYear()) {
      newErrors.year_built = `Year must be between 1800 and ${new Date().getFullYear()}`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: keyof PropertyData, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  return (
    <Card className="p-6 md:p-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="address" className="text-base font-semibold">
            Property Address *
          </Label>
          <Input
            id="address"
            placeholder="123 Main St, City, State ZIP"
            value={formData.address}
            onChange={(e) => handleChange("address", e.target.value)}
            className={errors.address ? "border-destructive" : ""}
            disabled={loading}
          />
          {errors.address && <p className="text-sm text-destructive">{errors.address}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="price" className="text-base font-semibold">
              Price ($) *
            </Label>
            <Input
              id="price"
              type="number"
              placeholder="450000"
              value={formData.price || ""}
              onChange={(e) => handleChange("price", Number(e.target.value))}
              className={errors.price ? "border-destructive" : ""}
              disabled={loading}
            />
            {errors.price && <p className="text-sm text-destructive">{errors.price}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="sqft" className="text-base font-semibold">
              Square Feet *
            </Label>
            <Input
              id="sqft"
              type="number"
              placeholder="1800"
              value={formData.sqft || ""}
              onChange={(e) => handleChange("sqft", Number(e.target.value))}
              className={errors.sqft ? "border-destructive" : ""}
              disabled={loading}
            />
            {errors.sqft && <p className="text-sm text-destructive">{errors.sqft}</p>}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <Label htmlFor="bedrooms" className="text-base font-semibold">
              Bedrooms
            </Label>
            <Select
              value={String(formData.bedrooms)}
              onValueChange={(value) => handleChange("bedrooms", Number(value))}
              disabled={loading}
            >
              <SelectTrigger id="bedrooms">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {[1, 2, 3, 4, 5, 6].map((num) => (
                  <SelectItem key={num} value={String(num)}>
                    {num}
                  </SelectItem>
                ))}
                <SelectItem value="7">6+</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="bathrooms" className="text-base font-semibold">
              Bathrooms
            </Label>
            <Select
              value={String(formData.bathrooms)}
              onValueChange={(value) => handleChange("bathrooms", Number(value))}
              disabled={loading}
            >
              <SelectTrigger id="bathrooms">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {[1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6].map((num) => (
                  <SelectItem key={num} value={String(num)}>
                    {num}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="year_built" className="text-base font-semibold">
              Year Built *
            </Label>
            <Input
              id="year_built"
              type="number"
              placeholder="2020"
              value={formData.year_built || ""}
              onChange={(e) => handleChange("year_built", Number(e.target.value))}
              className={errors.year_built ? "border-destructive" : ""}
              disabled={loading}
            />
            {errors.year_built && <p className="text-sm text-destructive">{errors.year_built}</p>}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="property_type" className="text-base font-semibold">
            Property Type
          </Label>
          <Select
            value={formData.property_type}
            onValueChange={(value) => handleChange("property_type", value)}
            disabled={loading}
          >
            <SelectTrigger id="property_type">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="House">House</SelectItem>
              <SelectItem value="Condo">Condo</SelectItem>
              <SelectItem value="Townhouse">Townhouse</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <Button type="submit" size="lg" className="w-full text-lg font-semibold" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              AI is analyzing your property...
            </>
          ) : (
            "Analyze Property"
          )}
        </Button>
      </form>
    </Card>
  );
};

export default PropertyForm;
