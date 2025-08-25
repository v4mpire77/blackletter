export async function uploadContract(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/jobs/`, {
    method: "POST",
    body: formData,
  });

  if (res.ok) {
    return await res.json();
  }
  return null;
}