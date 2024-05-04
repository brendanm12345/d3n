import React from 'react';
import fs from 'fs';
import path from 'path';
import { PatchRenderer } from '@/components/PatchRenderer';

const PullRequestPage = () => {
    const patchFilePath = path.join(process.cwd(), 'example.patch');
    const patchFileContent = fs.readFileSync(patchFilePath, 'utf-8');

    return (
        <div className='p-4 gap-2'>
            <h1 className='text-2xl'>Pull Request</h1>
            <PatchRenderer patchFile={patchFileContent} />
        </div>
    );
};

export default PullRequestPage;
