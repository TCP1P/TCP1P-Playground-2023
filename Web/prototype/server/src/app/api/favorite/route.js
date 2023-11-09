"use server"
import { NextResponse } from "next/server"

export async function POST(req) {
    const favorites = {}
    const account = {}
    const { favorite, reason } = await req.json()
    if (!favorite || !reason) {
        return NextResponse.json({ "message": "favorite or reason missing in form body" })
    }
    Object.assign(favorites[favorite], reason)
    if (account.role == "admin") {
        return NextResponse.json({ flag: process.env.FLAG })
    }
    return NextResponse.json(account)
}
