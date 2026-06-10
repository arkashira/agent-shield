- log_tool_call() {
+ log_tool_call() {
    agent_id=$(get_agent_id)
    tool_name=$1
    input_output=$(get_input_output)
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    status=$2

    log_message=$(jq -n \
        --arg agent_id "$agent_id" \
        --arg tool_name "$tool_name" \
        --arg input_output "$input_output" \
        --arg timestamp "$timestamp" \
        --arg status "$status" \
        '{agent_id: $agent_id, tool_name: $tool_name, input_output: $input_output, timestamp: $timestamp, status: $status}')

    log_file=$(get_log_file)
    echo "$log_message" >> "$log_file"
}