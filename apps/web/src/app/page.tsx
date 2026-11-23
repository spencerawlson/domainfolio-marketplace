import { formatPrice } from "@/lib/format";

/**
 * Homepage shell. The search bar and listing sections are real UI
 * wired to empty states: the marketplace has no inventory yet, and
 * this page must never show fabricated domains, sales figures, or
 * testimonials. Sections fill in as P0 stages land.
 */
export default function Home() {
  return (
    <div className="space-y-12">
      <section className="py-8 text-center">
        <h1 className="text-4xl font-bold tracking-tight">
          Find the domain your business deserves
        </h1>
        <p className="mx-auto mt-3 max-w-2xl text-neutral-600">
          Buy and sell domains with verified ownership and secure escrow.
          Every listing is verified before it goes live.
        </p>
        <form
          action="/browse"
          method="get"
          className="mx-auto mt-6 flex max-w-xl gap-2"
        >
          <input
            type="search"
            name="q"
            placeholder="Search domains…"
            aria-label="Search domains"
            className="flex-1 rounded-md border border-neutral-300 px-4 py-2"
          />
          <button
            type="submit"
            className="rounded-md bg-neutral-900 px-5 py-2 text-white"
          >
            Search
          </button>
        </form>
      </section>

      <section>
        <h2 className="text-2xl font-semibold">Featured domains</h2>
        <p className="mt-2 text-neutral-600">
          No featured listings yet. Featured listings are a paid,
          opt-in placement — they activate only after approval, and
          only for verified sellers.
        </p>
      </section>

      <section>
        <h2 className="text-2xl font-semibold">Recently listed</h2>
        <p className="mt-2 text-neutral-600">
          No domains listed yet. When sellers verify ownership and list
          a domain, it appears here.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-neutral-200 p-4">
          <h3 className="font-semibold">Verified ownership</h3>
          <p className="mt-1 text-sm text-neutral-600">
            A listing never activates without a DNS ownership check.
          </p>
        </div>
        <div className="rounded-lg border border-neutral-200 p-4">
          <h3 className="font-semibold">Secure escrow</h3>
          <p className="mt-1 text-sm text-neutral-600">
            Payments are held by a licensed escrow provider until the
            transfer is confirmed. Example price display:{" "}
            {formatPrice(333000)}.
          </p>
        </div>
        <div className="rounded-lg border border-neutral-200 p-4">
          <h3 className="font-semibold">Transparent fees</h3>
          <p className="mt-1 text-sm text-neutral-600">
            You see the full price and fees before you commit. Commission
            rates are published, versioned, and auditable.
          </p>
        </div>
      </section>
    </div>
  );
}
