import type { Metadata } from "next";
import "@genlayer/transaction-kit-react/styles.css";
import "./globals.css";
export const metadata: Metadata = { title:"PatchProof | Ship against the spec", description:"Validator-reviewed implementation evidence for acceptance criteria." };
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
