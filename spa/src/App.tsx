import { useCallback, useState, VFC } from "react";
import prettyBytes from "pretty-bytes";

interface UploadResult {
  chunkSizes: number[];
  totalSize: number;
  maxSize: number;
  minSize: number;
}

export const App: VFC = () => {
  const [file, setFile] = useState<File | null>(null);
  const onChangeFile = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setFile(event.target.files?.item(0) ?? null);
    },
    [setFile]
  );

  const [uploading, setUploading] = useState<boolean>(false);
  const [result, setResult] = useState<UploadResult>();

  const upload = useCallback(() => {
    setUploading(true);
    fetch("/api/", { method: "POST", body: file })
      .then((res) => res.json())
      .then((result) => setResult(result))
      .finally(() => setUploading(false));
  }, [file, setResult, setUploading]);

  return (
    <>
      <input type="file" onChange={onChangeFile} />
      <button disabled={uploading || !file} onClick={upload}>
        Upload
      </button>

      {result ? (
        <>
          <h3>Chunks</h3>
          <ul>
            {result.chunkSizes.map((size) => (
              <li
                style={{
                  color:
                    size === result.minSize
                      ? "blue"
                      : size === result.maxSize
                      ? "red"
                      : undefined,
                }}
              >
                {prettyBytes(size)}
              </li>
            ))}
          </ul>

          <h3>Summary</h3>
          <p>
            <b>Total:</b>
            {prettyBytes(result.totalSize)}
          </p>
          <p>
            <b>Max:</b>
            {prettyBytes(result.maxSize)}
          </p>
          <p>
            <b>Min:</b>
            {prettyBytes(result.minSize)}
          </p>
        </>
      ) : null}
    </>
  );
};
