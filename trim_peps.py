import csv, os

with open('app/data/peps_full.csv', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    rows = []
    for row in reader:
        name = row.get('name', '').strip()
        if name:
            rows.append({
                'name': name,
                'aliases': row.get('aliases', ''),
                'position': row.get('position', ''),
                'countries': row.get('countries', ''),
            })

with open('app/data/peps.csv', 'w', newline='', encoding='utf-8') as f:
    import csv as csv2
    writer = csv2.DictWriter(f, fieldnames=['name','aliases','position','countries'])
    writer.writeheader()
    writer.writerows(rows)

print('Records: ' + str(len(rows)))
print('Size: ' + str(round(os.path.getsize('app/data/peps.csv') / 1024 / 1024, 1)) + ' MB')
