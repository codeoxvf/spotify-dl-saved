<script context="module">
	import { accessToken } from './stores';
	import { get } from 'svelte/store';

	import ChoosePlaylist from './_components/ChoosePlaylist.svelte';

	export async function load() {
		if (!get(accessToken)) {
			return {
				status: 302,
				redirect: '/login'
			};
		}

		return {};
	}
</script>

<script lang="ts">
	const authorizationHeader: RequestInit = {
		headers: {
			Authorization: 'Bearer ' + $accessToken
		}
	};

	const playlists = fetch('https://api.spotify.com/v1/me/playlists', authorizationHeader).then(
		(res) => res.json()
	);
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
	{#await playlists}
		Loading...
	{:then data}
		<ChoosePlaylist {data} />
	{:catch error}
		<div class="alert alert-danger" role="alert">
			{error}
		</div>
	{/await}
</div>
