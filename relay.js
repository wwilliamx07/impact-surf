import express from "express"
import cors from "cors"
import { readFileSync } from "fs"
import { GoogleGenAI } from "@google/genai"

const app = express()
const port = 3000

app.use(cors())
app.use(express.json())

const key = readFileSync("secret.json").toString()
const gemini = new GoogleGenAI({ apiKey: key })

app.get("/relay", async (req, res) => {
    try {
        if (req.headers["url"] && req.headers["name"] && req.headers["address"]) {
            const response = await gemini.models.generateContent({
                model: "gemini-2.5-flash",
                contents: `Give a brief overview of this Canadian charity, 50 words max. Do not add any extra formatting. If not enough information can be found to give a meaningful response, output an empty string. Here are the details of the organization: Name: ${req.headers["name"]} Address: ${req.headers["address"]} Website: ${req.headers["url"]}`
            })

            if (response.text !== "") {
                res.send(response.text)
            } else {
                res.send("AI overview is not available for this organization.")
            }
        } else {
            res.status(200).send("200")
        }
    } catch (err) {
        console.error(err)
        res.status(500).send("Error generating AI overview.")
    }
})

app.listen(port, () => {
    console.log(`Server running at http://127.0.0.1:${port}`)
})
