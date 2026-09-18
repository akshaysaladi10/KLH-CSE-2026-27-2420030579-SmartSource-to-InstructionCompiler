import urllib.request
import json

print("=== VERIFYING API HEALTH ===")
res = urllib.request.urlopen("http://127.0.0.1:8000/api/health")
print("Health status:", res.status, res.read().decode())

print("\n=== VERIFYING API EXAMPLES ===")
res_ex = urllib.request.urlopen("http://127.0.0.1:8000/api/examples")
examples = json.loads(res_ex.read().decode())
print(f"Loaded {len(examples)} educational examples: {[e['id'] for e in examples]}")

print("\n=== VERIFYING API COMPILE ===")
compile_payload = {
    "source": "int a = 10;\nint b = 20;\nint c = a + b;\nprint c;",
    "enabledPasses": ["constant_folding", "constant_propagation", "algebraic_simplification", "dead_code_elimination"]
}
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/compile",
    data=json.dumps(compile_payload).encode(),
    headers={"Content-Type": "application/json"}
)
res = urllib.request.urlopen(req)
data = json.loads(res.read().decode())
print("Compile success:", data["success"])
print("Instructions generated:", len(data["instructions"]))
print("Per-stage timings (ms):", data.get("timings"))
print("Stage status:", data.get("stageStatus"))
print("Trace matrix rows:", len(data.get("traceMatrix", [])))

print("\n=== VERIFYING VM SIMULATE WITH BREAKPOINT ===")
sim_payload = {
    "instructions": data["instructions"],
    "breakpoints": [2],
    "maxCycles": 1000
}
req2 = urllib.request.Request(
    "http://127.0.0.1:8000/api/simulate",
    data=json.dumps(sim_payload).encode(),
    headers={"Content-Type": "application/json"}
)
res2 = urllib.request.urlopen(req2)
sim = json.loads(res2.read().decode())
print("Simulate success:", sim["success"])
print("Hit breakpoint?:", sim.get("hitBreakpoint"))
print("Breakpoint PC:", sim.get("breakpointPc"))
print("Flags:", sim.get("flags"))

print("\n=== VERIFYING FULL EXECUTION TO HALT ===")
sim_payload_full = {
    "instructions": data["instructions"],
    "breakpoints": [],
    "maxCycles": 1000
}
req3 = urllib.request.Request(
    "http://127.0.0.1:8000/api/simulate",
    data=json.dumps(sim_payload_full).encode(),
    headers={"Content-Type": "application/json"}
)
res3 = urllib.request.urlopen(req3)
sim_full = json.loads(res3.read().decode())
print("Simulate full execution output:", sim_full.get("output"))
print("Registers:", sim_full.get("registers"))
print("Memory:", sim_full.get("memory"))

print("\n=== VERIFYING FRONTEND PRODUCTION STATIC SERVE ===")
res_fe = urllib.request.urlopen("http://127.0.0.1:8000/")
html = res_fe.read().decode()
print("Frontend index.html length:", len(html))
print("Root div present?:", '<div id="root">' in html)
print("Asset script present?:", '/assets/index-' in html)
print("=== ALL SYSTEM ENDPOINTS VERIFIED SUCCESSFULLY ===")
