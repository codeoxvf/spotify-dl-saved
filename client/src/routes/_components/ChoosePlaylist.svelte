<script context="module">
	import { selectedPlaylist } from '../stores';
</script>

<script lang="ts">
	export let data: any;
</script>

<div class="container my-3">
	<div class="btn-group-vertical" role="group" aria-label="Select playlist">
		<div>Choose a playlist to download:</div>

		{#each data.items as playlist (playlist.id)}
			<input
				type="radio"
				class="btn-check"
				on:click={() => selectedPlaylist.set(playlist.id)}
				id={playlist.id}
				name="playlist"
			/>
			<label class="btn btn-outline-primary" for={playlist.id}>
				{playlist.name}
			</label>
		{/each}
	</div>

	<a class="btn btn-primary my-3" href="/download">Continue</a>
</div>
