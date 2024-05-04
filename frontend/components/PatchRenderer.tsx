import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { github } from 'react-syntax-highlighter/dist/esm/styles/prism';
import fs from 'fs';
import path from 'path';

interface PatchRendererProps {
    patchFile: string;
}

export const PatchRenderer: React.FC<PatchRendererProps> = ({ patchFile }) => {
    const lines = patchFile.split('\n');

    return (
        <div>
            {lines.map((line: string, index: React.Key | null | undefined) => {
                const isAddition = line.startsWith('+');
                const isDeletion = line.startsWith('-');
                const isHeader = line.startsWith('@@');
                const isFilename = line.startsWith('diff --git');

                let className = '';
                if (isAddition) className = 'addition';
                if (isDeletion) className = 'deletion';
                if (isHeader) className = 'header';
                if (isFilename) className = 'filename';

                return (
                    <div key={index} className={className}>
                        <SyntaxHighlighter language="diff" style={github}>
                            {line}
                        </SyntaxHighlighter>
                    </div>
                );
            })}
        </div>
    );
};