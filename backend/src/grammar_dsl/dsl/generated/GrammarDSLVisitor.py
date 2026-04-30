# Generated from C:/GITHUB/Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing/backend/src/grammar_dsl/dsl/grammar/GrammarDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GrammarDSLParser import GrammarDSLParser
else:
    from GrammarDSLParser import GrammarDSLParser

# This class defines a complete generic visitor for a parse tree produced by GrammarDSLParser.

class GrammarDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GrammarDSLParser#command.
    def visitCommand(self, ctx:GrammarDSLParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def visitGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#generateExerciseCmd.
    def visitGenerateExerciseCmd(self, ctx:GrammarDSLParser.GenerateExerciseCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#quantitySpec.
    def visitQuantitySpec(self, ctx:GrammarDSLParser.QuantitySpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#createQuizCmd.
    def visitCreateQuizCmd(self, ctx:GrammarDSLParser.CreateQuizCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#submitAnswersCmd.
    def visitSubmitAnswersCmd(self, ctx:GrammarDSLParser.SubmitAnswersCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#answerEntry.
    def visitAnswerEntry(self, ctx:GrammarDSLParser.AnswerEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#answerSeparator.
    def visitAnswerSeparator(self, ctx:GrammarDSLParser.AnswerSeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#answerValue.
    def visitAnswerValue(self, ctx:GrammarDSLParser.AnswerValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#showStudentsCmd.
    def visitShowStudentsCmd(self, ctx:GrammarDSLParser.ShowStudentsCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#showResultsCmd.
    def visitShowResultsCmd(self, ctx:GrammarDSLParser.ShowResultsCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#showQuizCmd.
    def visitShowQuizCmd(self, ctx:GrammarDSLParser.ShowQuizCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#showClassCmd.
    def visitShowClassCmd(self, ctx:GrammarDSLParser.ShowClassCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#studentFilterExpr.
    def visitStudentFilterExpr(self, ctx:GrammarDSLParser.StudentFilterExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#studentFilterOrExpr.
    def visitStudentFilterOrExpr(self, ctx:GrammarDSLParser.StudentFilterOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#studentFilterAndExpr.
    def visitStudentFilterAndExpr(self, ctx:GrammarDSLParser.StudentFilterAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#studentFilterPrimary.
    def visitStudentFilterPrimary(self, ctx:GrammarDSLParser.StudentFilterPrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#comparisonExpr.
    def visitComparisonExpr(self, ctx:GrammarDSLParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#statusExpr.
    def visitStatusExpr(self, ctx:GrammarDSLParser.StatusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def visitRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#historyCmd.
    def visitHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def visitResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#spellCmd.
    def visitSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#verbCmd.
    def visitVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#synonymCmd.
    def visitSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#helpCmd.
    def visitHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#featureExpr.
    def visitFeatureExpr(self, ctx:GrammarDSLParser.FeatureExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#featureOrExpr.
    def visitFeatureOrExpr(self, ctx:GrammarDSLParser.FeatureOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#featureAndExpr.
    def visitFeatureAndExpr(self, ctx:GrammarDSLParser.FeatureAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#featurePrimary.
    def visitFeaturePrimary(self, ctx:GrammarDSLParser.FeaturePrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#tense.
    def visitTense(self, ctx:GrammarDSLParser.TenseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#aspect.
    def visitAspect(self, ctx:GrammarDSLParser.AspectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#voice.
    def visitVoice(self, ctx:GrammarDSLParser.VoiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#sentenceType.
    def visitSentenceType(self, ctx:GrammarDSLParser.SentenceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#clauseStructure.
    def visitClauseStructure(self, ctx:GrammarDSLParser.ClauseStructureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#grammaticalFeature.
    def visitGrammaticalFeature(self, ctx:GrammarDSLParser.GrammaticalFeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#paragraph.
    def visitParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#sentence.
    def visitSentence(self, ctx:GrammarDSLParser.SentenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#sentencePart.
    def visitSentencePart(self, ctx:GrammarDSLParser.SentencePartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GrammarDSLParser#sentenceTerminator.
    def visitSentenceTerminator(self, ctx:GrammarDSLParser.SentenceTerminatorContext):
        return self.visitChildren(ctx)



del GrammarDSLParser