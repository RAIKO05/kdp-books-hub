def kdp_print_cost(pages):
    return 1.00 + (pages * 0.012)

def kdp_royalty(price, cost):
    return (price * 0.60) - cost

retail_10 = 10 * 12.99
print(f"Retail value of 10 individual books: ${retail_10:.2f}")

for pages in [700, 750, 800]:
    cost = kdp_print_cost(pages)
    print(f"\nSingle Book containing all 10 books ({pages} pages) | Amazon Print Cost: ${cost:.2f}")
    for p in [29.99, 34.99, 39.99, 44.99, 49.99]:
        roy = kdp_royalty(p, cost)
        disc = (1 - (p / retail_10)) * 100
        print(f"  Price: ${p:.2f} (Save {disc:.1f}%) -> Net Profit: ${roy:.2f} per sale")
