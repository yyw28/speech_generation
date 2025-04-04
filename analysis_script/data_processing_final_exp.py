# Apply same logic to all grouped sections like Q2.4.1–12, Q5.4.1–12, etc.

# Identify all groups present in filename_df that follow the QX.4.Y pattern
from collections import defaultdict

# Gather groupings
grouped_orders = defaultdict(list)
for order in filename_df['order']:
    if re.match(r'^\d+\.\d+\.\d+$', str(order)):
        group_key = '.'.join(str(order).split('.')[:2])
        grouped_orders[group_key].append(str(order))

# Compute pairwise speaker counts for each group
def compute_all_pairwise_counts(grouped_orders):
    all_pairwise_counts = {}
    for group_key in grouped_orders:
        group_counts = {}
        for i in range(2, 13, 2):  # even indices
            col = f"Q{group_key}.{i}.1"
            a_count = 0
            b_count = 0
            if col in results_df.columns:
                vals = results_df[col].dropna().astype(str).str.strip()
                a_count = vals.str.contains("Speaker A").sum()
                b_count = vals.str.contains("Speaker B").sum()
            group_counts[i] = {"A": a_count, "B": b_count}
        all_pairwise_counts[group_key] = group_counts
    return all_pairwise_counts

# Get speaker counts across all groups
all_pairwise_speaker_counts = compute_all_pairwise_counts(grouped_orders)

# Update filename_df accordingly
final_full_grouped_responses = []

for idx, row in filename_df.iterrows():
    order = str(row['order'])
    speaker = str(row['speaker']).strip()

    if re.match(r'^\d+\.\d+$', order):  # Simple questions
        question_key = f"Q{order}"
        if question_key in results_df.columns:
            count = results_df[question_key].apply(lambda x: speaker in str(x)).sum()
            final_full_grouped_responses.append(str(count))
        else:
            final_full_grouped_responses.append("")

    elif re.match(r'^\d+\.\d+\.\d+$', order):  # Grouped questions
        group_key = '.'.join(order.split('.')[:2])
        order_suffix = int(order.split('.')[-1])
        pair_second = order_suffix if order_suffix % 2 == 0 else order_suffix + 1

        if group_key in all_pairwise_speaker_counts:
            group_counts = all_pairwise_speaker_counts[group_key]
            if pair_second in group_counts:
                count = group_counts[pair_second].get(speaker, 0)
                final_full_grouped_responses.append(str(count))
            else:
                final_full_grouped_responses.append("0")
        else:
            final_full_grouped_responses.append("0")
    else:
        final_full_grouped_responses.append("")

# Apply final responses
filename_df['response'] = final_full_grouped_responses

# Show updated DataFrame
tools.display_dataframe_to_user(name="Fully Updated Grouped Responses (All Sets)", dataframe=filename_df)

