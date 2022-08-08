function main(params) {
  if (params.reviewId) {
    return {
      entries: params.rows
        .filter((row) => row.doc.id === params.reviewId)
        .map((row) => {
          return {
            id: row.id,
            name: row.doc.name,
            dealership: row.doc.dealership,
            review: row.doc.review,
            purchase: row.doc.purchase,
            purchase_date: row.doc.purchase_date,
            car_make: row.doc.car_make,
            car_model: row.doc.car_model,
            car_year: row.doc.car_year,
          };
        }),
    };
  }
  return {
    entries: params.rows.map((row) => {
      return {
        id: row.id,
        name: row.doc.name,
        dealership: row.doc.dealership,
        review: row.doc.review,
        purchase: row.doc.purchase,
        purchase_date: row.doc.purchase_date,
        car_make: row.doc.car_make,
        car_model: row.doc.car_model,
        car_year: row.doc.car_year,
      };
    }),
  };
}
