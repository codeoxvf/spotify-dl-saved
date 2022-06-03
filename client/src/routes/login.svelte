<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	import LoginButton from './_components/LoginButton.svelte';

	import { accessToken } from './stores';

	const REDIRECT_URI = 'http://localhost:3000/login/';

	const code = $page.url.searchParams.get('code');

	const loginUrl =
		'https://accounts.spotify.com/authorize?' +
		new URLSearchParams({
			client_id: 'bfc50500728c4b15a278734a930a735c',
			response_type: 'code',
			redirect_uri: REDIRECT_URI,
			scope: 'playlist-read-private'
		}).toString();

	let getToken: Promise<Response>;

	if (code) {
		getToken = fetch(
			'http://localhost:5000/?' +
				new URLSearchParams({
					code: code,
					redirect_uri: REDIRECT_URI
				})
		).then((res) => res.json());
	}

	function handleData(data: any): void {
		accessToken.set(data.access_token);
		goto('/');
	}
</script>

<svelte:head>
	<link
		href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
		rel="stylesheet"
		integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
		crossorigin="anonymous"
	/>
</svelte:head>

<div class="container my-3">
	{#if !code}
		<LoginButton {loginUrl} />
	{:else}
		{#await getToken}
			<div class="alert alert-secondary" role="alert">Loading...</div>
		{:then data}
			{handleData(data)}
		{:catch error}
			<div class="alert alert-danger" role="alert">
				{error}
			</div>
		{/await}
	{/if}
</div>
