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
	const playlists = fetch(
		'http://localhost:5000/download?' +
			new URLSearchParams({
				playlist_id: $selectedPlaylist,
				access_token: $accessToken
			})
	)
		.then((res) => res.json())
		.then((data) => {});
</script>
