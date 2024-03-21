import { get } from 'axios';

async function getSteamStats(username, apiKey, flags) {
    const baseUrl = 'https://api.steampowered.com/';  // Steam Web API base URL
    try {
        const response = await get(`${baseUrl}ISteamUser/GetPlayerSummaries/v2/?key=${apiKey}&steamids=${username}`);
        const data = response.data.response.players[0];

        // Extract and format relevant stats based on flags
        const formattedStats = {
            'Total Games': data.game_count,
            'Hours Played': Math.floor(data.playtime_forever / 60),
        };
        return formattedStats;
    } catch (error) {
        console.error('Error fetching Steam stats:', error);
    }
}

export async function handler(event, context) {
    try {
        const { username, flags } = JSON.parse(event.body);
        const apiKey = process.env.STEAM_API_KEY;
        const apiKeyFromSecret = process.env.GITHUB_WORKFLOW_STEAM_API_KEY;  // Access secret
        const apiKeyToUse = apiKeyFromSecret || apiKey;  // Fallback to local env var (for testing)
        const stats = await getSteamStats(username, apiKeyToUse, flags);
        return {
            statusCode: 200,
            body: JSON.stringify(stats),
        };
    } catch (error) {
        console.error('Error processing request:', error);
    }
}
