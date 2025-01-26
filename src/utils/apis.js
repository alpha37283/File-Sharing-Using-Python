export async function fetchFiles(path) {
  const response = await fetch(`/api/files?path=${encodeURIComponent(path)}`);
  if (!response.ok) {
    throw new Error("Failed to fetch files");
  }
  return await response.json();
}
