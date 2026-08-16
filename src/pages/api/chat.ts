export const prerender = false; // 👈 Tells Astro to execute this file on the server, not at build time

import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    // 1. Parse the incoming prompt from your front-end chat component
    const { prompt } = await request.json();

    if (!prompt) {
      return new Response(
        JSON.stringify({ error: 'Prompt is required' }), 
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // 2. Forward the payload securely to your live Cloud Run service
    const cloudRunUrl = 'https://rag-backend-489381507990.europe-west1.run.app/api/v1/query';
    const backendResponse = await fetch(cloudRunUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      return new Response(
        JSON.stringify({ error: `Backend engine responded with status ${backendResponse.status}` }), 
        { status: backendResponse.status, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // 3. Extract the answer and stream it back cleanly to the browser
    const data = await backendResponse.json();
    return new Response(
      JSON.stringify({ answer: data.answer }), 
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Proxy route error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error processing the chat request.' }), 
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};