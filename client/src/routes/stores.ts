import { writable } from 'svelte/store';

export const accessToken = writable('');
export const selectedPlaylist = writable('');