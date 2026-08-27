import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Home } from 'lucide-react';
import Header from '@/components/Header';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { getPlansByCategory, getMediaUrl } from '@/api';

const formatPrice = (price) => {
  const amount = Number(price);
  if (Number.isNaN(amount)) return price;
  return `Ksh ${amount.toLocaleString()}`;
};

export default function BrowsePage() {
  const { category } = useParams();
  const decodedCategory = decodeURIComponent(category || '');
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!decodedCategory) return;

    setLoading(true);
    setError(null);

    getPlansByCategory(decodedCategory)
      .then(setPlans)
      .catch(() => setError('Could not load plans for this category.'))
      .finally(() => setLoading(false));
  }, [decodedCategory]);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <section className="pt-28 pb-16 px-6 bg-slate-50 flex-1">
        <div className="max-w-7xl mx-auto">
          <div className="mb-10">
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight mb-2">
              {decodedCategory} Plans
            </h1>
            <p className="text-slate-600">
              Browse house plans posted by designers in this category.
            </p>
          </div>

          {loading && (
            <p className="text-slate-500">Loading plans...</p>
          )}

          {error && (
            <p className="text-red-600">{error}</p>
          )}

          {!loading && !error && plans.length === 0 && (
            <div className="text-center py-16 bg-white rounded-xl shadow-sm">
              <Home className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-600 mb-2">No plans found in this category yet.</p>
              <p className="text-slate-400 text-sm">
                Designers can add new categories when they post a plan.
              </p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {plans.map((plan) => (
              <Card
                key={plan.id}
                className="group overflow-hidden rounded-xl border-0 shadow-xl shadow-slate-200/50 hover:shadow-2xl transition-all duration-500 bg-white"
              >
                <div className="relative h-64 overflow-hidden bg-slate-200">
                  <img
                    src={getMediaUrl(plan.thumbnail) || '/images/hero.png'}
                    alt={plan.title}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                  <div className="absolute top-4 left-4 z-10">
                    <Badge className="bg-primary text-white border-0 rounded-md px-3 text-xs uppercase">
                      {plan.category_group}
                    </Badge>
                  </div>
                </div>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold text-slate-800 line-clamp-1">{plan.title}</h3>
                    <span className="font-bold text-primary pl-2 text-lg whitespace-nowrap">
                      {formatPrice(plan.price)}
                    </span>
                  </div>
                  {plan.seller_name && (
                    <p className="text-sm text-slate-500 mb-4">By {plan.seller_name}</p>
                  )}
                  <p className="text-sm text-slate-600 line-clamp-2 mb-6">
                    {plan.description || 'No description provided.'}
                  </p>
                  <Button className="w-full rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-medium py-6">
                    View Plan Details
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
