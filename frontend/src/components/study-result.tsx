"use client";

import type { ReactNode } from "react";

type StudyResultProps = {
  text: string;
};

type Block =
  | { type: "heading"; level: 1 | 2 | 3; text: string }
  | { type: "section"; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[] };

export function StudyResult({ text }: StudyResultProps) {
  const blocks = parseBlocks(text);

  if (blocks.length === 0) {
    return <p className="study-output__empty">No output yet.</p>;
  }

  return (
    <div className="study-output">
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          if (block.level === 1) {
            return (
              <h2 key={index} className="study-output__title">
                {renderInline(block.text)}
              </h2>
            );
          }

          if (block.level === 2) {
            return (
              <h3 key={index} className="study-output__subtitle">
                {renderInline(block.text)}
              </h3>
            );
          }

          return (
            <h4 key={index} className="study-output__minor-title">
              {renderInline(block.text)}
            </h4>
          );
        }

        if (block.type === "section") {
          return (
            <h4 key={index} className="study-output__section-label">
              {renderInline(block.text)}
            </h4>
          );
        }

        if (block.type === "list") {
          return (
            <ul key={index} className="study-output__list">
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex}>{renderInline(item)}</li>
              ))}
            </ul>
          );
        }

        return (
          <p key={index} className="study-output__paragraph">
            {renderInline(block.text)}
          </p>
        );
      })}
    </div>
  );
}

function parseBlocks(text: string): Block[] {
  const lines = text
    .replace(/\r\n/g, "\n")
    .split("\n")
    .map((line) => line.trim());

  const blocks: Block[] = [];
  let paragraphBuffer: string[] = [];
  let listBuffer: string[] = [];

  const flushParagraph = () => {
    if (paragraphBuffer.length > 0) {
      blocks.push({
        type: "paragraph",
        text: paragraphBuffer.join(" "),
      });
      paragraphBuffer = [];
    }
  };

  const flushList = () => {
    if (listBuffer.length > 0) {
      blocks.push({
        type: "list",
        items: [...listBuffer],
      });
      listBuffer = [];
    }
  };

  for (const line of lines) {
    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);
    if (headingMatch) {
      flushParagraph();
      flushList();
      blocks.push({
        type: "heading",
        level: headingMatch[1].length as 1 | 2 | 3,
        text: headingMatch[2],
      });
      continue;
    }

    const sectionMatch = line.match(/^\*\*(.+)\*\*$/);
    if (sectionMatch) {
      flushParagraph();
      flushList();
      blocks.push({
        type: "section",
        text: sectionMatch[1],
      });
      continue;
    }

    const listMatch = line.match(/^-+\s+(.*)$/);
    if (listMatch) {
      flushParagraph();
      listBuffer.push(listMatch[1]);
      continue;
    }

    flushList();
    paragraphBuffer.push(line);
  }

  flushParagraph();
  flushList();

  return blocks;
}

function renderInline(text: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  const pattern = /(\*\*[^*]+\*\*|\*[^*]+\*|\[\d+\])/g;
  let lastIndex = 0;
  let key = 0;

  for (const match of text.matchAll(pattern)) {
    const token = match[0];
    const index = match.index ?? 0;

    if (index > lastIndex) {
      nodes.push(text.slice(lastIndex, index));
    }

    if (token.startsWith("**") && token.endsWith("**")) {
      nodes.push(<strong key={key++}>{token.slice(2, -2)}</strong>);
    } else if (token.startsWith("*") && token.endsWith("*")) {
      nodes.push(<em key={key++}>{token.slice(1, -1)}</em>);
    } else {
      nodes.push(
        <span key={key++} className="study-output__citation-token">
          {token}
        </span>
      );
    }

    lastIndex = index + token.length;
  }

  if (lastIndex < text.length) {
    nodes.push(text.slice(lastIndex));
  }

  return nodes;
}
