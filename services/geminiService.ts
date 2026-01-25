
import { GoogleGenAI, Type } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });

export const getAthleteInsight = async (athleteName: string) => {
  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 ${athleteName} 提供一段简短且鼓舞人心的总结（最多50字）。重点介绍他们的专长和一个有趣的小知识。请使用专业的体育评论员语调，并使用中文回复。`,
      config: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
      },
    });
    return response.text;
  } catch (error) {
    console.error("Gemini Error:", error);
    return "龙的精神在冰面上高高飞扬。祝我们的运动员好运！";
  }
};

export const getEventPrediction = async (eventTitle: string) => {
    try {
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: `预测冬奥会项目 "${eventTitle}" 中运动员面临的主要技术挑战。字数控制在60字以内，请使用中文回复。`,
      });
      return response.text;
    } catch (error) {
      return "在这项极具挑战性的冬季项目中，技术精度和心理韧性将是获胜的关键。";
    }
};
