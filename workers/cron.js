/**
 * Cloudflare Worker for autocash-ultimate cron jobs
 * 
 * This worker runs scheduled tasks for content generation
 * Configure trigger: Cron Triggers in Cloudflare dashboard
 * Example: "0 */12 * * *" (every 12 hours)
 */

export default {
  async scheduled(event, env, ctx) {
    const API_URL = env.API_URL || 'https://yourdomain.com';
    const ADMIN_TOKEN = env.ADMIN_TOKEN;
    
    // Check kill switch
    const healthCheck = await fetch(`${API_URL}/health`);
    const health = await healthCheck.json();
    
    if (health.kill_switch) {
      console.log('Kill switch enabled - skipping generation');
      return;
    }
    
    // Trigger batch generation
    try {
      const response = await fetch(`${API_URL}/api/batch-generate`, {
        method: 'POST',
        headers: {
          'Authorization': `****** ${ADMIN_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          count: 5,
          review_required: true
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Batch generation successful:', result);
      } else {
        console.error('Batch generation failed:', response.status);
      }
    } catch (error) {
      console.error('Error during batch generation:', error);
    }
  },

  async fetch(request, env, ctx) {
    return new Response('Autocash Worker - Use cron triggers', { status: 200 });
  }
};
