<template>
  <div class="w-full max-w-2xl mx-auto bg-slate-900 border border-slate-800 rounded-xl shadow-2xl overflow-hidden flex flex-col h-[500px]">
    <!-- Header -->
    <div class="px-6 py-4 bg-slate-850 border-b border-slate-800 flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
        <h3 class="text-sm font-semibold text-slate-200 tracking-wide uppercase">
          William Power AI Assistant
        </h3>
      </div>
      <span class="text-xs text-slate-400 font-mono">RAG v1.0</span>
    </div>

    <!-- Messages Container -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin scrollbar-thumb-slate-800">
      <div 
        v-for="(message, index) in messages" 
        :key="index"
        :class="['flex w-full max-w-[85%] rounded-lg p-4 text-sm leading-relaxed', 
                 message.role === 'user' 
                   ? 'ml-auto bg-indigo-600 text-white rounded-br-none' 
                   : 'bg-slate-800 text-slate-300 rounded-bl-none']"
      >
        <div class="whitespace-pre-wrap">{{ message.text }}</div>
      </div>

      <!-- Loading / Typing Indicator -->
      <div v-if="isLoading" class="flex w-max max-w-[85%] bg-slate-800 text-slate-400 rounded-lg rounded-bl-none p-4 text-sm items-center space-x-2">
        <span>Thinking</span>
        <div class="flex space-x-1">
          <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-100"></div>
          <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-250"></div>
          <div class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-500"></div>
        </div>
      </div>
    </div>

    <!-- Input Form -->
    <form @submit.prevent="sendMessage" class="p-4 bg-slate-850 border-t border-slate-800 flex items-center space-x-3">
      <input
        v-model="inputMessage"
        type="text"
        placeholder="Ask about William's background, cloud experience..."
        :disabled="isLoading"
        class="flex-1 bg-slate-950 text-slate-200 placeholder-slate-500 text-sm rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 border border-slate-800"
      />
      <button
        type="submit"
        :disabled="isLoading || !inputMessage.trim()"
        class="bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm px-5 py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-1"
      >
        <span>Send</span>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

// With this:
const CLOUD_RUN_URL = 'https://portfolio-rag-backend-489381507990.europe-west1.run.app/api/v1/query';

const messages = ref<Message[]>([
  { role: 'assistant', text: "Hello! I'm William's background assistant. Ask me anything about his cloud architecture, Java systems, or platform engineering experience." }
]);
const inputMessage = ref('');
const isLoading = ref(false);
const chatContainer = ref<HTMLDivElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  const prompt = inputMessage.value.trim();
  if (!prompt || isLoading.value) return;

  messages.value.push({ role: 'user', text: prompt });
  inputMessage.value = '';
  isLoading.value = true;
  await scrollToBottom();

  try {
    const response = await fetch(CLOUD_RUN_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });

    if (response.status === 429) {
      throw new Error('Rate limit reached (5 requests/hour limit). Please try again later.');
    }

    if (!response.ok) {
      throw new Error(`Server error (${response.status})`);
    }

    const data = await response.json();
    const answerText = data.answer || data.response || 'No response returned.';

    messages.value.push({ role: 'assistant', text: answerText });
  } catch (error: any) {
    messages.value.push({ 
      role: 'assistant', 
      text: `⚠️ ${error.message || 'Connection error. Please try again later.'}` 
    });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};
</script>