generator target {
    output_type "python/pydantic"
    output_dir ".."
    version "0.84.4"
    default_client_mode async
}

client<llm> Default {
  provider openai
  options {
    model gpt-4.1
  }
}
