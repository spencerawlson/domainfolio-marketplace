import { describe, expect, it } from "vitest";
import { formatPrice, leaseMonthly } from "../src/lib/format";

describe("formatPrice", () => {
  it("formats cents as whole dollars with separators", () => {
    // en-CA distinguishes USD from CAD: "US$3,330", not "$3,330".
    expect(formatPrice(333000)).toBe("US$3,330");
    expect(formatPrice(100)).toBe("US$1");
  });
});

describe("leaseMonthly", () => {
  it("rounds up, never down", () => {
    expect(leaseMonthly(333000, 12)).toBe(27750);
    expect(leaseMonthly(100, 3)).toBe(34);
  });

  it("rejects a non-positive term", () => {
    expect(() => leaseMonthly(100, 0)).toThrow();
  });
});
