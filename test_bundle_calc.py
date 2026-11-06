def kdp_print_cost(pages):
    return 1.00 + (pages * 0.012)

def kdp_royalty(list_price, print_cost):
    return (list_price * 0.60) - print_cost

print("=== EXACT KDP BUNDLE ECONOMICS ===")
single_price = 12.99
single_cost = kdp_print_cost(176)
single_royalty = kdp_royalty(single_price, single_cost)
print(f"Single Book (176 pgs): Price=${single_price:.2f} | Print=${single_cost:.2f} | Profit=${single_royalty:.2f}")

print("\n--- 10-BOOK SERIES (e.g. The Grand Orient Express) ---")
ten_retail = 10 * single_price
print(f"Retail Total (10 books @ $12.99): ${ten_retail:.2f}")

# Model A: Sold individually through KDP Series 1-Click
# If each individual book is priced at $7.99 for bundle buyers:
price_a = 7.99
royalty_a = kdp_royalty(price_a, single_cost)
total_price_a = price_a * 10
total_profit_a = royalty_a * 10
disc_a = (1.0 - (total_price_a / ten_retail)) * 100
print(f"\nModel A: 10 Individual Books via KDP Series Page @ ${price_a:.2f} ea:")
print(f"  Total Customer Price: ${total_price_a:.2f} (Save {disc_a:.1f}%)")
print(f"  Your Net Profit:       ${total_profit_a:.2f}")

# Model B: Two 5-Book Master Omnibus Editions (Vols 1-5 & Vols 6-10)
# Page count ~600 pages per book
comp_cost = kdp_print_cost(600)
print(f"\nModel B: Two 5-Book Deluxe Omnibus Volumes (~600 pgs each, print cost=${comp_cost:.2f}):")
for p in [24.99, 29.99, 34.99]:
    r = kdp_royalty(p, comp_cost)
    total_p = p * 2
    total_prof = r * 2
    disc = (1.0 - (total_p / ten_retail)) * 100
    print(f"  Price ${p:.2f} per volume -> Series Bundle: ${total_p:.2f} (Save {disc:.1f}%) -> Net Profit: ${total_prof:.2f}")

print("\n--- 15-BOOK SERIES (e.g. Detective's Case Files, Project X, etc.) ---")
fifteen_retail = 15 * single_price
print(f"Retail Total (15 books @ $12.99): ${fifteen_retail:.2f}")

# Model A: 15 individual books @ $7.99
total_price_15a = price_a * 15
total_profit_15a = royalty_a * 15
disc_15a = (1.0 - (total_price_15a / fifteen_retail)) * 100
print(f"\nModel A: 15 Individual Books via KDP Series @ ${price_a:.2f} ea:")
print(f"  Total Customer Price: ${total_price_15a:.2f} (Save {disc_15a:.1f}%)")
print(f"  Your Net Profit:       ${total_profit_15a:.2f}")

# Model B: Three 5-Book Deluxe Omnibus Volumes (Vols 1-5, 6-10, 11-15)
print(f"\nModel B: Three 5-Book Deluxe Omnibus Volumes (~600 pgs each):")
for p in [24.99, 27.99, 29.99, 34.99]:
    r = kdp_royalty(p, comp_cost)
    total_p = p * 3
    total_prof = r * 3
    disc = (1.0 - (total_p / fifteen_retail)) * 100
    print(f"  Price ${p:.2f} per volume -> Full 15-Book Series: ${total_p:.2f} (Save {disc:.1f}%) -> Net Profit: ${total_prof:.2f}")

# Model C: Complete 15-Book Digital Box Set (Kindle eBook)
print(f"\nModel C: Complete 15-Book Digital Omnibus (Kindle / e-Reader, Print Cost=$0.00):")
for ep in [19.99, 24.99, 29.99]:
    # At > $9.99, KDP eBook royalty is 35%
    er = ep * 0.35
    edisc = (1.0 - (ep / fifteen_retail)) * 100
    print(f"  Digital Price: ${ep:.2f} (Save {edisc:.1f}%) -> Your Net Profit: ${er:.2f} (Zero Print Cost!)")
