import { useCallback, useState, VFC } from "react";
import prettyBytes from "pretty-bytes";

interface UploadResult {
  chunkSizes: number[];
  totalSize: number;
  maxSize: number;
  minSize: number;
}

export interface InvalidSchema {
  index: number;
  data: any;
  errors: {
    loc: string[];
    msg: string;
    type: string;
  }[];
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
    fetch("/api/", {
      method: "POST",
      body: file,
      headers: { "Content-Type": "application/json" },
      // @ts-ignore See https://web.dev/fetch-upload-streaming/
      allowHTTP1ForStreamingUpload: true,
    })
      .then(async (res) => {
        const result = await res.json();
        switch (res.status) {
          case 200:
            setResult(result);
            break;
          case 400:
            console.log(result);
            break;
          default:
            break;
        }
      })
      .finally(() => setUploading(false));
  }, [file, setResult, setUploading]);

  return (
    <>
      <input
        type="file"
        disabled={uploading}
        onChange={onChangeFile}
      />
      <button disabled={uploading} onClick={upload}>
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
