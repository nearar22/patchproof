import { createAccount, createClient, isSuccessful } from "genlayer-js";
import { studioDevnet } from "genlayer-js/chains";
const raw = process.env.GENLAYER_PRIVATE_KEY?.trim(), contract = process.env.CONTRACT_ADDRESS?.trim();
if (!raw || !contract) throw new Error("GENLAYER_PRIVATE_KEY and CONTRACT_ADDRESS are required");
const chain = { ...studioDevnet, id: 61997, rpcUrls: { default: { http: ["https://studio-next.genlayer.com/api"] } } };
const client = createClient({ chain, account: createAccount(raw.startsWith("0x") ? raw : `0x${raw}`) });
const id = process.env.DEMO_CASE_ID || "author-safety-audit";
const spec = "https://raw.githubusercontent.com/nearar22/threadmark/992484c4d145c4c0d3d82e94c248e097714637c6/README.md";
const patch = "https://raw.githubusercontent.com/nearar22/threadmark/992484c4d145c4c0d3d82e94c248e097714637c6/contracts/threadmark.py";
async function write(label, functionName, args, intelligent = false) {
  const fees = await client.estimateTransactionFees({ leaderTimeunitsAllocation: intelligent ? 500n : 180n, validatorTimeunitsAllocation: intelligent ? 600n : 360n });
  const hash = await client.writeContract({ address: contract, functionName, args, fees }); console.log(`${label}_TX=${hash}`);
  const receipt = await client.waitForTransactionReceipt({ hash, waitUntil: "finalized", retries: 300, interval: 3000, fullTransaction: true });
  const status = String(receipt.statusName ?? receipt.status ?? "unknown"), execution = String(receipt.txExecutionResultName ?? receipt.txExecutionResult ?? "unknown"), consensus = String(receipt.resultName ?? receipt.result_name ?? "unknown");
  console.log(`${label}_STATUS=${status};EXECUTION_RESULT=${execution};CONSENSUS=${consensus}`);
  if (!isSuccessful(receipt) || status !== "FINALIZED" || execution !== "FINISHED_WITH_RETURN" || consensus === "MAJORITY_DISAGREE") throw new Error(`${label} failed`); return hash;
}
await write("OPEN", "open_case", [id, "Author safety remediation", spec, ["Validate every author wallet before changing state.", "Allow only the board owner to manage authors."]]);
await write("SUBMIT", "submit_revision", [id, "revision-one", patch, "Implements strict wallet normalization and owner-only author management."]);
await write("INSPECT", "inspect_revision", [id, "revision-one"], true);
const state = await client.readContract({ address: contract, functionName: "get_revision", args: [id, "revision-one"], jsonSafeReturn: true });
console.log(`LIVE_STATE=${JSON.stringify(state)}`);
if (!["READY", "NEEDS_WORK"].includes(state.status) || !state.result?.source_receipts?.length) throw new Error("Stored result missing");
