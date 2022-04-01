<script lang="ts">
	export let data;
</script>

<div class="container">
	<div class="btn-group-vertical" role="group" aria-label="Select playlist">
		<div>Choose a playlist to download:</div>

		{#each data.items as playlist}
			<div class="btn btn-primary">{playlist.name}</div>
		{/each}
	</div>
</div>
