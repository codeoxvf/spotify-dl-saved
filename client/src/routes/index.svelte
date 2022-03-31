<script lang="ts">
	import { page } from '$app/stores';

	const CLIENT_ID = 'bfc50500728c4b15a278734a930a735c';
	const SCOPE = 'playlist-read-private';
	const REDIRECT_URI = 'http://localhost:3000/';
	const SERVER = 'http://localhost:5000/';

	const params = $page.url.searchParams;

	const loginUrl =
		'https://accounts.spotify.com/authorize?' +
		new URLSearchParams({
			client_id: CLIENT_ID,
			response_type: 'code',
			redirect_uri: REDIRECT_URI,
			scope: SCOPE
		}).toString();

	function handleData(data) {
	}
</script>

{#if !params.has('code')}
	<a href={loginUrl}> Login on Spotify to authorise the app </a>
{:else}
	{#await fetch(SERVER + '?' + new URLSearchParams({
		code: params.get('code'),
		redirect_uri: REDIRECT_URI
	}))}
		Authenticating...
	{:then response}
		{#await response.json()}
			Loading...
		{:then data}
			{handleData(data)}
		{:catch error}
			{error}
		{/await}
	{:catch error}
		{error}
	{/await}
{/if}