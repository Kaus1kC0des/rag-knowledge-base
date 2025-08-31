import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from "rehype-sanitize";


export const customDesigns = {
    h1: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h1 className="text-2xl font-bold mt-4 mb-2" {...props} />
    ),
    h2: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h2 className="text-xl font-semibold mt-3 mb-1" {...props} />
    ),
    h3: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h3 className="text-lg font-semibold mt-2 mb-1" {...props} />
    ),
    p: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <p className="text-sm leading-relaxed mb-2" {...props} />
    ),
    code({ inline, className, children, ...props }:{
        inline?: boolean; 
        className?: string; 
        children: React.ReactNode; 
    }) {
    const match = /language-(\w+)/.exec(className || "");
    return !inline && match ? (
        <pre className="p-3 rounded bg-gray-900 text-gray-100 overflow-x-auto">
        <code className={className} {...props}>
            {children}
        </code>
        </pre>
    ) : (
        <code
        className="bg-gray-200 dark:bg-gray-800 px-1 rounded"
        {...props}
        >
        {children}
        </code>
    );
    },
    table: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <table className="table-auto border-collapse border border-gray-400 my-4 w-full text-sm" {...props} />
    ),
    thead: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <thead className="" {...props} />
    ),
    th: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <th className="border border-gray-400 px-3 py-2 text-left font-semibold" {...props} />
    ),
    td: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <td className="border border-gray-300 dark:border-gray-700 px-3 py-2" {...props} />
    ),
    tr: (props: React.HTMLAttributes<HTMLHeadingElement>) => (
    <tr className="" {...props} />
    ),
}


export default function Markdown({children}:{children:string;}){
    
    return(
        <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw,rehypeSanitize]} components={customDesigns}>
        {children}
        </ReactMarkdown>
    )
}