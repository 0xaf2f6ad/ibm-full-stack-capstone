function main(params) {
  const data = params.review;
  if (!data.name || !data.comment || !data.dealership) {
    return Promise.reject({ error: "incomplete fields passed" });
  }
  return {
    doc: {
      createdAt: new Date(),
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    },
  };
}

