export const prerender = false; // 👈 Ensures dynamic server execution in hybrid mode

import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json().catch(() => ({}));
    const { prompt } = body;

    if (!prompt) {
      return new Response(
        JSON.stringify({ error: 'Prompt is required' }), 
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const cloudRunUrl = 'https://rag-backend-489381507990.europe-west1.run.app/api/v1/query';
    
    const backendResponse = await fetch(cloudRunUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    if (!backendResponse.ok) {
      const errorDetail = await backendResponse.text();
      console.error('Cloud Run Error Detail:', errorDetail);
      return new Response(
        JSON.stringify({ error: `Backend service error (${backendResponse.status})` }), 
        { status: backendResponse.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const data = await backendResponse.json();
    return new Response(
      JSON.stringify({ answer: data.answer }), 
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Proxy Exception:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error processing the chat request.' }), 
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};