import requests
import ray

def send_query(text, host, model):
    host += model.replace("/", "--")
    print(f"Sending query '{text}' to '{host}'")
    resp = requests.post(host, json={"prompt": text})
    try:
        return model, resp.json()[model]["generated_text"]
    except Exception:
        return model, resp.text

send_query_remote = ray.remote(send_query).options(num_cpus=0)

def send_queries_ray(text, output_boxes, host):
    pending_refs = []
    for k, v in output_boxes.items():
        if v.visible:
            pending_refs.append(send_query_remote.remote(text, host, k))
            yield {v: ""}
    while pending_refs:
        ready_refs, pending_refs = ray.wait(pending_refs, num_returns=1)
        if ready_refs:
            ready_refs = ray.get(ready_refs)
            for model, response in ready_refs:
                yield {output_boxes[model]: response}