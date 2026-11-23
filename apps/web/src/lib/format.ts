/** Price formatting for listing displays. Amounts are integer cents;
 * display is dollars with thousands separators (en-CA). */

export function formatPrice(cents: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(cents / 100);
}

/** Lease-to-own monthly figure: ceiling division, never a fixed split. */
export function leaseMonthly(priceCents: number, months: number): number {
  if (months <= 0) throw new Error("lease term must be positive");
  return Math.ceil(priceCents / months);
}
