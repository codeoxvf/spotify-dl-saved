<script context="module">
	import { selectedPlaylist, accessToken } from './stores';
	import { get } from 'svelte/store';
	import { SvelteComponentTyped } from 'svelte';

	export async function load() {
		if (!get(selectedPlaylist) || !get(accessToken)) {
			return {
				status: 302,
				redirect: '/'
			};
		}

		return {};
	}
</script>

<script lang="ts">
	const playlist = fetch(
		'http://localhost:5000/download?' +
			new URLSearchParams({
				playlist_id: $selectedPlaylist,
				access_token: $accessToken
			})
	)
		.then((res) => res.blob())
		.then((blob) => URL.createObjectURL(blob));
</script>

<svelte:head>
	<link
		href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
		rel="stylesheet"
		integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
		crossorigin="anonymous"
	/>
</svelte:head>

{#await playlist}
	Loading...
{:then url}
	<a href={url} download={$selectedPlaylist + '.zip'} class="btn btn-primary">Download</a>
{/await}
